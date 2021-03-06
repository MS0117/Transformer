# -*- coding: utf-8 -*-
"""dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xcYgZp7rS0UD9IYF5SXFUcpZ0bMCqeD_
"""

import torch
from torch.utils.data import Dataset, DataLoader
from tokenizer import SentencePieceTokenizer
import logging
LOGGER = logging.getLogger()

class CustomDataset(Dataset):
    def __init__(self, tokenizer, max_seq_len, datapath, langpair, type='train'):
      srclang=langpair.split('-')[0]                                           #파일 불러오기
      trglang=langpair.split('-')[1]
      f=open("{}/{}.{}.{}".format(datapath,type,langpair,srclang),encoding='utf-8')
      src=f.readlines()                                                         #src은 train.de-en.de파일의 모든 문자열, 줄 별로 인덱스   
      
      f=open("{}/{}.{}.{}".format(datapath,type,langpair,trglang),encoding='utf-8')
      trg=f.readlines()
      assert(len(src)==len(trg))

      self.max_seq_len=max_seq_len
      self.length=len(src)
      self.input=src
      self.output=trg
      self.tokenizer=tokenizer

    def __len__(self):
      return self.length  

    def __getitem__(self, idx):
      input=self.input[idx]
      output=self.output[idx]
  
      return torch.tensor(self.tokenizer.Encode(input),dtype=torch.float64, requires_grad=True), torch.tensor(self.tokenizer.Encode(output),dtype=torch.float64, requires_grad=True)      #getitem을 통해 input을 인덱스별로 데이터를 가져온다. torch.Tensor(class)과 torch.tensor(function)은 다름. 받는 인자부터 다르다


    def collate_fn(self,data):                                                  #dataset의 sample은 각각 length가 다름, padding해서, length 맞춰주기 위한 함수
      """data는 튜플을 element로 한 list이다. [([1,2,3],[4,5]),([6,7],[8,9])] 튜플의
      element는 정수화된 src, trg sequence"""

      def merge(sentences):
        new_sentences=torch.zeros(len(sentences),self.max_seq_len,requires_grad=True).long()
        if torch.cuda.is_available():
                new_sentences = new_sentences.cuda()
        for i, sentence in enumerate(sentences):
          new_sentences[i][:min(self.max_seq_len,len(sentence))]=sentence[:min(self.max_seq_len,len(sentence))]

        return new_sentences  


      data.sort(key=lambda x:len(x[0]),reverse=True)                            #첫번째,(soruce sentence)의 길이를 기준으로 정렬)                          

      source_sentences,target_sentences=zip(*data)                              #([1,2,3],[6,7])  ([4,5],[8,9])로 나뉨
      src=merge(source_sentences)
      trg=merge(target_sentences)

      return src,trg

def init_logging():
    LOGGER.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s: [ %(message)s ]',
                            '%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    LOGGER.addHandler(console)

def test():
    init_logging()
    datapath = './datasets/iwslt14.de.en'
    tokenizer = SentencePieceTokenizer(datapath).loadmodel()

    # en_tokenizer.load_model()
    dataset = CustomDataset(type='valid', tokenizer=tokenizer, 
                         max_seq_len=10, datapath=datapath, langpair='de-en')
    train_loader = DataLoader(dataset=dataset,
                              batch_size=1,
                              shuffle=False,
                              collate_fn=dataset.collate_fn)
    for epoch in range(10):
        for i, data in enumerate(train_loader):
            inputs, outputs = data
            print("inputs.size()=",outputs.size())
            LOGGER.info("inputs.size()=".format(inputs.size()))
            LOGGER.info(inputs)
            print("outputs.size()=",outputs.size())
            LOGGER.info("outputs.size()=".format(outputs.size()))
            LOGGER.info(outputs)
            break
if __name__ == "__main__":
    test()