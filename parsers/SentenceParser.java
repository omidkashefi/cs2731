import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.OutputStream;

public interface SentenceParser {
	public SentenceTree createSentenceTree(String sent);
	public void printSentenceDependencies(String filename, OutputStream out, int numToParse) throws FileNotFoundException, IOException;
}
