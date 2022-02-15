# Transformer
Reimplementation of [Attention Is All You Need](https://arxiv.org/abs/1706.03762) 

## Download Datasets
Using IWSLT14 de-en
```
$ download.sh
```

## SentencePiece Tokenizer
```
$ python tokenizer.py --vocab_size 16000
```

## Train model
```
$ MODEL_NAME="transformer"
$ python main.py --mode train \
                 --datapath './datasets/iwslt14.de.en'\
                 --langpair 'de-en'\                 
                 --model_name ${MODEL_NAME}
```

## Evaluate model
```
MODEL_NAME="transformer"
INPUT_NAME="./iwslt14-de-en.in"
OUTPUT_NAME="./iwslt14-de-en.out"
python main.py --mode test \
    --model_name ${MODEL_NAME} \
    --eval_input ${INPUT_NAME} \
    --eval_output ${OUTPUT_NAME}
    
sacrebleu ref.detok.txt -i iwslt14-de-en.out.txt -m bleu -b -w 4    
```    
    
