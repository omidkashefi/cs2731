import java.util.List;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.StringReader;

import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;


public class StanfordParser implements SentenceParser {
	LexicalizedParser lp;
	
	public StanfordParser() {
		String parserModel = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		lp = LexicalizedParser.loadModel(parserModel);
	}

	@Override
	public SentenceTree createSentenceTree(String sent) {
	    TokenizerFactory<CoreLabel> tokenizerFactory =
	        PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
	    Tokenizer<CoreLabel> tok =
	        tokenizerFactory.getTokenizer(new StringReader(sent));
	    List<CoreLabel> rawWords2 = tok.tokenize();
	    Tree parse = lp.apply(rawWords2);
	    
	    TreebankLanguagePack tlp = lp.treebankLanguagePack(); // PennTreebankLanguagePack for English
	    GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
	    GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
	    List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
	    
	    SentenceTree tree = new SentenceTree(rawWords2.size()+1);
	    tree.wordDependence[0] = 0;
	    
	    for (TypedDependency dep : tdl) {
	    	int index = dep.dep().index();
	    	int parent = dep.gov().index();
	    	tree.wordDependence[index] =  parent;
	    }
		
		return tree;
	}

	@Override
	public void printSentenceDependencies(String filename, OutputStream out, int numToParse) throws FileNotFoundException, IOException {
		// iterate over sentences and output them
		File file = new File(filename);
		int sentenceId = 0;
		try (BufferedReader br = new BufferedReader(new FileReader(file))) {
			BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out));
		    String line;
		    while ((line = br.readLine()) != null && sentenceId < numToParse) {
		    	//System.out.println(line);
		    	if (line.trim().length() > 0) {
		    		System.out.println(line);
			    	writer.write(Integer.toString(sentenceId) + ":" + createSentenceTree(line).toString());
			    	writer.write("\n");		    		
		    	}
				sentenceId++;
		    } 
		    writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
