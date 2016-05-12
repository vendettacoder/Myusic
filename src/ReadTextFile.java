import java.io.*;
import java.util.*;

public class ReadTextFile{

  public static void main(String[] args) throws IOException{
    String pwd = getCurrentDirectory();
    ArrayList<ArrayList<String>> allSongs = new ArrayList<ArrayList<String>>();
    try{
      File path = new File(pwd+"/../Songs");
      File[] files = path.listFiles();
      Arrays.sort(files);
      for(int i=0;i<files.length;i++){
        if(files[i].isFile()){
          String fileName = files[i].getName();
          String filePath = pwd + "/../Songs/" + fileName;
          allSongs.add(getSongWordList(filePath));
          System.out.println("One file processed..");
        }
      }
      HashMap<String,Integer> dictionary = new HashMap<String,Integer>();
      dictionary = generateDictionary(allSongs);
      int numSongs = allSongs.size();
      int corpusSize = dictionary.size();
      int vectorizedMatrix[][] = new int[numSongs][corpusSize];
      for(int i=0;i<numSongs;i++){
        ArrayList<String> song = allSongs.get(i);
        for(String word : song){
          vectorizedMatrix[i][dictionary.get(word)]++;
        }
      }
      printToFile(vectorizedMatrix,numSongs,corpusSize);
    }
    catch(Exception e){
      System.out.println("Error while adding songs to allSongs:" + e.getMessage());
    }
  }

  public static void printToFile(int vectorizedMatrix[][],int numSongs,int corpusSize) throws IOException{
    FileOutputStream fileOut = null;
    try{
      fileOut = new FileOutputStream("Vectorized_Matrix.txt");
      for(int i=0;i<numSongs;i++){
        StringBuilder toFile = new StringBuilder();
        for(int element : vectorizedMatrix[i]) {
          toFile.append(element).append(" ");
        }
        fileOut.write(toFile.toString().trim().getBytes());
        fileOut.write("\n".getBytes());
      }
    }
    catch(Exception e){
      System.out.println("Error while writing vectorized matrix to file:" + e.getMessage());
    }
  }

  public static HashMap<String,Integer> generateDictionary(ArrayList<ArrayList<String>> allSongs) throws Exception{
    HashMap<String,Integer> dictionary = new HashMap<String,Integer>();
    int index = 0;
    for(ArrayList<String> song : allSongs){
      for(String word : song){
        if(!dictionary.containsKey(word)){
            dictionary.put(word,index++);
        }
      }
    }

    PrintWriter writer = new PrintWriter("dictionary.txt", "UTF-8");
    for (Map.Entry entry : dictionary.entrySet()) {
      writer.print("'"+entry.getKey()+"':"+entry.getValue()+",");
    }
    writer.close();
    return dictionary;
  }


  public static ArrayList<String> eliminateStopwords(String songText,String pwd) throws IOException{
    String stopWordsFile = pwd + "/Stopwords.txt";
    ArrayList<String> stopWords = new ArrayList();
    ArrayList<String> retVal = new ArrayList<>();
    try{
      FileReader inputFile = new FileReader(stopWordsFile);
      BufferedReader bufferReader = new BufferedReader(inputFile);
      String word;
      String allStopWords="";
      while((word = bufferReader.readLine())!=null){
        word = word.trim();
        if(word.length() != 0){
          allStopWords = allStopWords + " " + word;
        }
      }
      String[] stopWordsArray = allStopWords.replaceAll("[^a-zA-Z ]", "").toLowerCase().split("\\s+");
      for(String stopWord : stopWordsArray)
      {
        songText = songText.replaceAll(' '+stopWord+' ', "  ");
      }
      String[] songArr = songText.split("\\s+");
      retVal = new ArrayList(Arrays.asList(songArr));
    }
    catch(Exception e){
      System.out.println("Error while reading file line by line:" + e.getMessage());
    }
    return retVal;
  }

  public static String getCurrentDirectory(){
    String dir = System.getProperty("user.dir");
    return dir;
  }

  public static ArrayList<String> getSongWordList(String filePath) throws IOException{
    ArrayList<String> retVal = new ArrayList<>();
    try{
      FileReader inputFile = new FileReader(filePath);
      BufferedReader bufferReader = new BufferedReader(inputFile);
      String line;
      String song="";
      while((line = bufferReader.readLine())!=null){
        line = line.trim();
        if(line.length() != 0){
          song = song + " " + line;
        }
      }
      String songText = song.replaceAll("[^a-zA-Z ]", "").toLowerCase();
      String pwd = getCurrentDirectory();
      retVal = eliminateStopwords(songText,pwd);
      bufferReader.close();
    }
    catch(Exception e){
      System.out.println("Error while reading file line by line:" + e.getMessage());
    }
    return retVal;
  }
}
