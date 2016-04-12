import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.util.Arrays;

import org.maltparser.concurrent.ConcurrentMaltParserModel;
import org.maltparser.concurrent.ConcurrentMaltParserService;
import org.maltparser.concurrent.ConcurrentUtils;
import org.maltparser.concurrent.graph.ConcurrentDependencyGraph;
import org.maltparser.concurrent.graph.ConcurrentDependencyNode;

public class MaltParser implements SentenceParser {
	ConcurrentMaltParserModel model;

	public MaltParser() {
		try {
			URL modelURL = new File("/Users/janinelove/Desktop/maltparser-1.8.1/models/engmalt.linear-1.7.mco").toURI().toURL();
			model = ConcurrentMaltParserService.initializeParserModel(modelURL);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public SentenceTree createSentenceTree(String sent) {
		// TODO Auto-generated method stub
		return null;
	}

	private int getParentId(ConcurrentDependencyGraph graph, int id) {
		if (id == 0) return 0;
		ConcurrentDependencyNode node = graph.getDependencyNode(id);
		//System.out.println(node);
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(3)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(4)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(5)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(6)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(7)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(8)));
//		System.out.println(node.getLabel(graph.getDataFormat().getColumnDescription(9)));
		return node.getHeadIndex();
//		ColumnDescription column = graph.getDataFormat().getColumnDescription(9);
//		return Integer.parseInt(node.getLabel(column));
	}
	
	@Override
	public void printSentenceDependencies(String filename, OutputStream out, int numToParse) throws FileNotFoundException, IOException {
	   	BufferedReader reader = null;
    	BufferedWriter writer = null;
    	try {
    		reader = new BufferedReader(new InputStreamReader(new File(filename).toURI().toURL().openStream(), "UTF-8"));
    		writer = new BufferedWriter(new OutputStreamWriter(out));
    		int sentenceCount = 0;
    		while (true && sentenceCount < numToParse) {
    			// Reads a sentence from the input file
	    		String[] inputTokens = ConcurrentUtils.readSentence(reader);
	    		System.out.println(sentenceCount);
	    		System.out.println(Arrays.toString(inputTokens) + "\n");
	    		
	    		
	    		// If there are no tokens then we have reach the end of file
	    		if (inputTokens.length == 0) {
	    			sentenceCount++;
	    			continue;
	    		}

	    		// Parse the sentence
	    		ConcurrentDependencyGraph graph = model.parse(inputTokens);
	    		
	    		// Writes the sentence to the output file
	    		//ConcurrentUtils.writeSentence(outputTokens, writer);
	    		
	    		writer.write(Integer.toString(sentenceCount) + ":");
	    		for (int i = 0; i < inputTokens.length; i++) {
	    			writer.write(Integer.toString(i)+"-"+getParentId(graph, i) +",");
	    		}
	    		writer.write(Integer.toString(inputTokens.length)+"-"+ getParentId(graph,inputTokens.length));
	    		writer.write("\n");
	    		sentenceCount++;
    		}
    		//System.out.println("Parsed " + sentenceCount +" sentences");
    	} catch (Exception e) {
			e.printStackTrace();
    	} finally {
    		if (reader != null) {
    			try {
    				reader.close();
    	    	} catch (IOException e) {
    				e.printStackTrace();
    	    	}
    		}
    		if (writer != null) {
    			try {
    				writer.close();
    	    	} catch (IOException e) {
    				e.printStackTrace();
    	    	}
    		}
    	}
	}

}
