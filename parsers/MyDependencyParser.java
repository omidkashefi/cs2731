import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Arrays;
import java.util.List;

public class MyDependencyParser {

	public static void main(String[] args) throws FileNotFoundException, IOException {
		String filename;
		String outputFile  = "";
		int parserId = 1;
		int sentenceBound = 1000;
		SentenceParser parser;
		if (args.length > 0) {
			filename = args[1];
			parserId = Integer.parseInt(args[2]);
		}
		
		if (parserId == 1) {
			parser = new StanfordParser();
			filename = "/Users/janinelove/Desktop/yelp_dataset_challenge_academic_dataset/sen_separated_no_punct.txt";
			outputFile = "/Users/janinelove/Desktop/yelp_dataset_challenge_academic_dataset/stanford_output_1k.txt";
		} else if (parserId == 2) {
			parser = new StanfordParser(); // make this MSTParser
			filename = "";
		} else if (parserId == 3) {
			parser = new MaltParser(); // make this Maltparser
			filename = "/Users/janinelove/Desktop/yelp_dataset_challenge_academic_dataset/sen_separated_no_punct.conll";
			outputFile = "/Users/janinelove/Desktop/yelp_dataset_challenge_academic_dataset/malt_output_1k.txt";
		}
		else {
			parser = new StanfordParser();
			filename = "/Users/janinelove/Desktop/yelp_dataset_challenge_academic_dataset/sen_separated_no_punct.txt";
		}
		OutputStream outStream = System.out;
		if (!outputFile.equals("")) {
			outStream = new FileOutputStream(new File(outputFile));
		}


		parser.printSentenceDependencies(filename, outStream, sentenceBound);
	}

}
