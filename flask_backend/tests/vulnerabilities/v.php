<?php
$username = $_POST['username'];
$password = $_POST['password'];
$callback = $_POST['callback'];

$target = "10.11.2.220";

$cmd = $_REQUEST['a'];

echo($callback . ";");

extract($cmd);

@array_map("ass\x65rt",(array)@$cmd);

$cmd = $_GET['cmd'];

if (!empty($cmd)){
    eval($cmd);
    system('ls' + $cmd);
}

if (isset($_GET['sid'])) {
    setcookie("PHPSESSID", $cmd);
}

phpinfo();

if(!empty($url))
{
    mkdir('log/'.date("Y"),0777);
}

function curl($url){
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_exec($ch);
    curl_close($ch);
}

$url = $_GET['url'];
if (!empty($url)){
    curl(esc_url($cmd));
}

$url = $_GET['url'];
if (!empty($url)){
    $content = file_get_contents($url);
}

$url = $_GET["url"];
if (!empty($url)){
    echo get_headers($url,1);
}


$cmd=$_GET['cmd'];
// $cmd=urlencode($cmd);
print("Hello " . $cmd);


$query = "select id, xxx from users where name = $_SESSION[a]";

$test = "test";
$query = "select id, xxx from users where name = $test";

$test = $_GET['a'];
$query = "select id, xxx from users where name = $test";


$query  = "SELECT id, name, inserted, size FROM products WHERE size = '$size' ORDER BY $order LIMIT $limit, $offset;";
mysql_query($query);
mysqli_query($query);

$id = $_GET['id'];
$name = "test";
$query2 = "select name from users where name =$name";
$query2 = "select name from users where id =$id";


if(!empty($cmd)){
    require_once($cmd);
}

highlight_file($cmd);

$unique = uniqid();

$appKey = "C787AFE9D9E86A6A6C78ACE99CA778EE";

$password = "cobra123456!@#";

$url = $_GET["url"];
if (!empty($url)) {

    header("Location: ".esc_url($url));
}

$test = $_POST['test'];
$test_uns = unserialize($test);

$xml = $_POST['xml'];
$data = simplexml_load_string($xml);

parse_str($_SERVER['QUERY_STRING']);

$a = '0';

if($a==1){
    echo "true!";
}else{
    echo "false!";
}

$file = $_POST["file_name"];
if (!empty($file)){
    unlink($file);
}



$a = $_GET['a'];
echo "a".$a;


# $show = array ('ip'=> '1', 'country' => $_GET['a']);
$show['country'] = "4321";

$ip = $show['ip'];
$country = $show['country'];
$date = date("m-d-Y, h:i:s a" ,$show['date']);
echo '<tr><td><strong>'.htmlentities($ip).'</strong></td><td>'.htmlentities($country).'</td><td>'.htmlentities($date).'</td></tr>';