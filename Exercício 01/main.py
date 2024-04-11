from mrjob.job import MRJob
import re

palavras_regex = re.compile(r"[\w']+")
class ContaPalavra(MRJob):
    def mapper(self, _, linha):
        for palavra in palavras_regex.findall(linha):
            yield (palavra.lower(), 1)

    def reducer(self, palavra, contagem):
        yield palavra, sum(contagem)
if __name__ == "__main__":
    ContaPalavra.run()