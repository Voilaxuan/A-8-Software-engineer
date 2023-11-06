#rule_2000
DocumentBuilderFactory doc=DocumentBuilderFactory.newInstance();
DocumentBuilder db=doc.newDocumentBuilder();
InputStream is= new  FileInputStream("test.xml");    
Document doc=dombuilder.parse(is);   #injection 
Element rootElement = document.getDocumentElement();

SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();
XMLReader reader = parser.getXMLReader();   //reader.setContentHandler(new MyContentHandler());
reader.parse(xmlPath);    #injection 

#SSRF
// HttpURLConnection ssrf vul
String url = request.getParameter ( "url");
URL u = new URL(url);
URLConnection urlconnection = u.openConnection( );
HttpURLConnection httpUrl = (HttpURLConnection)urlConnection;
BufferedReader in = new BufferedReader(new InputStreamReader(httpUrl.getInputStream()));//String inputLine;
StringBuffer html = new StringBuffer();
while ( ( inputLine = in.readLine( )) != null) {
  html.append ( inputLine);
  }
System.out.println( "html : " + html.toString());
in.close();

String url = request.getParameter( "url");
okHttpclient client = new okHttpclient();
com.squareup.okhttp.Request ok_http = new com .squareup.okhttp.Request.Builder().url(ur1) .build() ;
client.newCall(ok_http).execute();

#command_exe
shell.evaluate("
static void main(String[]args){
  Runtime.getRuntime().exec(command);
  }
 
");


