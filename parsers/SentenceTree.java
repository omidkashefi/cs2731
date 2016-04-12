

public class SentenceTree {
	public int[] wordDependence;
	
	public SentenceTree(int size) {
		wordDependence = new int[size];
	}
	
	// output the tree for the sentence in the format that they wanted
	public String toString() {
		String val = "";
		for (int i = 0; i < wordDependence.length-1; i++) {
			val = val + Integer.toString(i) + "-" + wordDependence[i] + ",";
		}
		val = val + Integer.toString(wordDependence.length-1) + "-" + wordDependence[wordDependence.length-1];
		return val;
	}
}
