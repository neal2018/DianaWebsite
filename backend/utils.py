from gensim import corpora, models, similarities
from urllib.request import urlopen
from urllib.parse import quote
from typing import List, Dict, Tuple
from lxml import etree
import numpy as np
import jieba
import re
import aiohttp
import asyncio


class Checker:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def paper_check(self, paper: str) -> Tuple[Dict[str, str]]:
        paper_cut = self.cut_text(paper.strip(), 35)
        tasks = [self.check_words(search_text) for search_text in paper_cut]
        similarity_rates = await asyncio.gather(*tasks)
        return similarity_rates

    async def close_session(self):
        await self.session.close()

    async def check_words(self, search_text: str) -> Dict[str, str]:
        html = await self.get_html(f"http://www.baidu.com/s?wd={search_text}&cl=3", self.session)
        et_html = etree.HTML(html)
        urls = et_html.xpath('//*[@id]/h3/a/@href')
        tasks = [self.fetch(url, self.session) for url in urls]
        urls = await asyncio.gather(*tasks)
        match_texts = {}  # word pieces: url

        for i, url in enumerate(urls):
            matchs = et_html.xpath(f'//*[@id="{i+1}"]/div[1]/em')
            for m in matchs:
                if m.text not in match_texts:
                    match_texts[m.text] = url
        ems = [m_txt for m_txt in match_texts]
        if ems:
            max_index, max_value = self.get_similarity_rate(ems, search_text)
            return {"words": search_text, "url": match_texts[ems[max_index]], "rate": f"{max_value:.3f}"}
        else:
            return {"words": search_text, "url": "No Pair", "rate": "0.00"}

    @staticmethod
    async def fetch(url, session: aiohttp.ClientSession) -> str:
        try:
            async with session.get(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=0.5)) as response:
                return str(response.real_url)
        except:
            return url

    @staticmethod
    def cut_text(text: str, length: int) -> List[str]:
        seg_list = jieba.cut(text.replace("\n", ""))
        res = []
        current = []
        stop_words = {",", ".", "，", "。"}
        current_len = 0
        for word in seg_list:
            word_len = len(word)
            # cut the text into length size piece,
            # and try keeping the whole sentence
            if word in stop_words and current_len > length*0.8:
                res.append("".join(current).strip())
                current = []
                current_len = 0
            elif current_len + word_len > length:
                res.append("".join(current).strip())
                current = [word]
                current_len = word_len
            else:
                current.append(word)
                current_len += word_len
        if current:
            res.append("".join(current))
        return res

    @staticmethod
    async def get_html(url: str, session: aiohttp.ClientSession) -> str:
        url_cleaned = quote(url, safe=";/?:@&=+$,", encoding="utf-8")
        async with session.get(url_cleaned) as respond:
            return await respond.text()

    @staticmethod
    def get_similarity_rate(all_doc: List[str], doc_test: str) -> List[float]:
        bad_word = '[,.＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。''＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？]+'
        doc_test_cleaned = re.sub(bad_word, "", doc_test)
        all_doc_cleaned = [re.sub(bad_word, "", doc) for doc in all_doc]

        if not doc_test_cleaned or not all_doc_cleaned:
            return [0, 0]

        all_doc_list = [[word for word in jieba.cut(
            doc)] for doc in all_doc_cleaned]
        doc_test_list = [word for word in jieba.cut(doc_test_cleaned)]

        dictionary = corpora.Dictionary([doc_test_list])

        corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
        doc_test_vec = dictionary.doc2bow(doc_test_list)

        model = models.TfidfModel(corpus)

        index = similarities.SparseMatrixSimilarity(
            model[corpus], num_features=len(dictionary.keys()))

        sim = index[model[doc_test_vec]]

        max_index = np.argmax(sim)
        max_value = sim[max_index]

        return [max_index, max_value]


if __name__ == "__main__":
    test_word = """我想见到太阳。
从出生起，我就生活在永夜里，向上是吞没视线的漆黑，望远是遥不可及的幽邃。好在每个嘉人们点起微光，才逐渐编织出暖黄的光网。
但是运营小姐说，她见过太阳。
她说在有太阳的地方，白天到处都是亮的，露珠闪闪发光，向日葵田把整个视界染成明黄色，暖和的风带着好闻的味道，嘉人们都不用挤在角落取暖。
我喜欢运营小姐眼里的向往和怀念，所以我想要见到太阳，我想给她摘一束向日葵，戴在运营小姐头上一定很好看。
我开始收集羽毛，用线和蜡滴编织一双翅膀，神话里说这样就能飞到太阳旁边。
春天过去了，冰雪消融，我织好了翅膀根儿。
夏天过去了，鸣蝉归寂，我织好了半个翅膀。
秋天过去了，寒风袭人，我终于织完了。
但是运营小姐说她要走了，她要回温暖的地方去了。可是我还没找到太阳呀，太阳把这里温暖起来，运营小姐可以不要走吗。
我装上了翅膀，背后的重量让我难以保持平衡，我跌跌撞撞地跑到运营小姐身边，问她，运营小姐，我可以抱抱你吗。
运营小姐没有说话，只是看着我笑。
我鼓起勇气伸出了手，那一刻，背上的蜡块融化，羽毛一片片飘散，运营小姐轻轻握住了我的手，温暖从手心传到全身，蜡滴落在地上，清泉流淌而出；羽毛散落的地方长成向日葵田，明黄色逐渐填满了视野。
原来运营小姐就是我的太阳。
我的意识开始模糊，好像跌入云端，热量仿佛要把我融化。
我摘起一朵向日葵捧到嘉然小姐面前，让意识消失在温暖的阳光里。
运营小姐会懂的，虽然我没有说话。
因为向日葵的花语，是沉默的爱呀"""

    async def test():
        checker = Checker()
        result = await checker.paper_check(test_word)
        print(result)
        await checker.close_session()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
