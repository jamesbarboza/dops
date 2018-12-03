 corpus_root = "gmb-1.0.0"  #defining path of gmb corpus version 1.0.0
 reader = read_corpus(corpus_root) #reading it and removing unnecessary tags
 iob = to_iob_form(reader)	# adding IOB Tags B,I,O
 untagged = untag(iob)	#removing IOB tags 
 history = history(iob)	#storing IOB tags in separate array
 X = transform_into_dataset(untagged,history) #Getting features and converting into dataset
 ner = NER(X,history)
 ner.train(X[:limit],history[:limit])
 ner.tag("India is great nation") 


In Data/ner_instances/ner_object is NER object which is trained on 80k words , can be used directy by unpickling it and make sure that NER class is imported or started in the shell

