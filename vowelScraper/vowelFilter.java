import java.util.*;
import java.io.*;
import java.lang.*;

class vowelFilter {
	public static void main(String args[]) {
		ArrayList<Sample> dataOut = new ArrayList<>();
		ArrayList<Sample> contClearedOut = new ArrayList<>();
		ArrayList<Sample> finalOut = new ArrayList<>();
		try {
			 dataOut = readCSV(args[0]);
		}
		catch (FileNotFoundException e) {
			System.out.println(e);
		}
		

		int contRange = Integer.parseInt(args[2]); 
		double freqVariance = Double.parseDouble(args[3]);

		for (int i = 0; i < dataOut.size() - contRange; i++) {
			if (checkContinuity(dataOut, i, contRange, freqVariance)) {
				contClearedOut.add(dataOut.get(i));
			}
		}
		
		int thresh = Integer.parseInt(args[4]); // Threshold in dB
		for (Sample s : contClearedOut) {
			if (checkIntensity(s, thresh)) {
				finalOut.add(s);
			}
		}

		writeToOutput(args[1], finalOut);
	}



	private static ArrayList<Sample> readCSV(String filename) throws FileNotFoundException {
		ArrayList<Sample> dataOut = new ArrayList<>();

		Scanner scan = new Scanner(new File(filename));
		scan.useDelimiter("\n");
		while (scan.hasNext()) {
			dataOut.add(new Sample(scan.next()));
		}
		scan.close();

		return dataOut;
	}	


	private static boolean checkContinuity(ArrayList<Sample> listIn, int sampleIndex, int contRange, double contThresh) {
		if (!validateCheckCont(sampleIndex, contRange)) {
			//System.out.println("Range not sufficient. Choose a higher index to test");
			return false;
		}

		Sample[] checkArray = new Sample[(2 * contRange)];
		
		for (int i = 0; i < (2 * contRange); i++) {
			checkArray[i] = listIn.get((sampleIndex - contRange) + i);
		}

		Sample baseSample = listIn.get(sampleIndex);

		ArrayList<Sample> listOut = new ArrayList<>();
		for (Sample s : checkArray) {
			double diffF1 = Math.abs(baseSample.getF1() - s.getF1());
			double diffF2 = Math.abs(baseSample.getF2() - s.getF2());
			double diffF3 = Math.abs(baseSample.getF3() - s.getF3());
			double diffF4 = Math.abs(baseSample.getF4() - s.getF4());
			double diffF5 = Math.abs(baseSample.getF5() - s.getF5());
			//System.out.println(diffF2 + " " + diffF3 + " " + diffF4);
			 
			if (diffF1 > contThresh || diffF2 > contThresh || diffF3 > contThresh || diffF4 > contThresh || diffF5 > contThresh) {
				return false;
			}
		}	
		//System.out.println(checkArray[4].getF3());
		return true;
	}
	
	
	private static double getStdDev(Sample[] listIn, int formant) {
		double average = avg(listIn, formant);
		double sum = 0;

		for (Sample s : listIn) {
			double f = s.getFormant(formant);
			double variance = f - average;
			double varSquared = Math.pow(variance, 2);
			sum += varSquared;
		}

		return Math.sqrt(sum/listIn.length);
	}

	private static double avg(Sample[] listIn, int formant) {
		double sum = 0;
		for (int i = 0; i < listIn.length; i++) {
			sum += listIn[i].getFormant(formant);
		}
		return sum/listIn.length;
	}

	private static boolean validateCheckCont(int sampleIndex, int contRange) {
		int x = sampleIndex - contRange;
		if (x < 1) {
			return false;
		}
		return true;
	}


	private static boolean checkIntensity(Sample s, int threshold) {
		if (s.getIntensity() >= threshold) {
			// System.out.println(s.getIntensity());
			return true;
		}
		return false;
	}


	private static void writeToOutput(String filenameOut, ArrayList<Sample> toBeWritten) {
		try {
			PrintWriter writer = new PrintWriter(filenameOut, "UTF-8");
			for (Sample s : toBeWritten) {
				writer.println(s.toCSVString());
			}

			writer.close();
		}
		catch (IOException e) {
			System.out.println(e);
		}
	}
}



class Sample {
	private float time, intensity;
	private double f1, f2, f3, f4, f5;

	public Sample(String inString) {
		try {
			String[] splitData = inString.split(", ");
			this.time = Float.parseFloat(splitData[0]);
			this.intensity = Float.parseFloat(splitData[1]);
			this.f1 = Double.parseDouble(splitData[2]);
			this.f2 = Double.parseDouble(splitData[3]);
			this.f3 = Double.parseDouble(splitData[4]);
			this.f4 = Double.parseDouble(splitData[5]);
			this.f5 = Double.parseDouble(splitData[6]);			
		}		
		catch (Exception e) {
			System.out.println("No data in file!\n" + e);
		}
	}

	public String toCSVString() {
		return time + ", " + intensity + ", " + f1 + ", " + f2 + ", " + f3 + ", " + f4 + ", " + f5;
	}


	public float getTime() {
		return time;
	}
	public float getIntensity() {
		return intensity;
	}
	public double getF1() {
		return f1;
	}
	public double getF2() {
		return f2;
	}
	public double getF3() {
		return f3;
	}
	public double getF4() {
		return f4;
	}
	public double getF5() {
		return f5;
	}
	public double getFormant(int formant) {
		switch (formant) {
			case 1:
				return this.getF1();
			case 2:
				return this.getF2();
			case 3:
				return this.getF3();
			case 4: 
				return this.getF4();
			case 5:
				return this.getF5();
		}
		return 0;
	}
}
