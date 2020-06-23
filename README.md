# bert-lo-bleach
コミックLOとBLEACHのどちらのキャッチコピーかをBERTにあててもらう

# usage
```
#Juman++、こっちの方が良さそう
sudo  apt-get install libboost-all-dev google-perftools libgoogle-perftools-dev
wget "http://lotus.kuee.kyoto-u.ac.jp/nl-resource/jumanpp/jumanpp-1.02.tar.xz"
tar xJvf jumanpp-1.02.tar.xz
cd jumanpp-1.02
./configure
make
sudo make install
cd ../

# このリポジトリとbertのリポジトリのclone
git clone https://github.com/TtH61008/bert-lo-bleach.git    
git clone https://github.com/google-research/bert.git

# dataの前処理
python bert-lo-bleach/src/preprocess.py bert-lo-bleach/data/lo.tsv bert-lo-bleach/data/bleach.tsv bert-lo-bleach/data/concatted.tsv 

# BERT日本語モデルのダウンロード
wget "http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/JapaneseBertPretrainedModel/Japanese_L-12_H-768_A-12_E-30_BPE.zip&name=Japanese_L-12_H-768_A-12_E-30_BPE.zip"
unzip 'lime.cgi?down=http:%2F%2Fnlp.ist.i.kyoto-u.ac.jp%2Fnl-resource%2FJapaneseBertPretrainedModel%2FJapanese_L-12_H-768_A-12_E-30_BPE.zip&name=Japanese_L-12_H-768_A-12_E-30_BPE.zip'

# 207行目、text = self._tokenize_chinese_chars(text)をコメントアウト
cat bert/tokenization.py |sed "s/text = self._tokenize_chinese_chars(text)/#text = self._tokenize_chinese_chars(text)/g" > bert/tokenization.py

export BERT_BASE_DIR=Japanese_L-12_H-768_A-12_E-30_BPE
export DATA_DIR=bert-lo-bleach/preprocessed_data

python bert/run_classifier.py   \
    --task_name=CoLA\
    --do_train=true\
    --do_eval=true\
    --data_dir=$DATA_DIR\
    --vocab_file=$BERT_BASE_DIR/vocab.txt \
    --bert_config_file=$BERT_BASE_DIR/bert_config.json \
    --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
    --do_lower_case=False\
    --max_seq_length=128\
    --train_batch_size=32\
    --learning_rate=2e-5\
    --num_train_epochs=3.0\
    --output_dir=/tmp/cola_output/
```



# 参考
http://nlp.ist.i.kyoto-u.ac.jp/index.php?BERT%E6%97%A5%E6%9C%AC%E8%AA%9EPretrained%E3%83%A2%E3%83%87%E3%83%AB
https://techblog.nhn-techorus.com/archives/12978
