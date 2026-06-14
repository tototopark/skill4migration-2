<?php
$content = file_get_contents('f:/pe/public_html/test-migration/sitepro/index.php');
if (preg_match('/\$cHhVk\s*=\s*array\((.*?)\);\s*goto/s', $content, $matches)) {
    // PHP 코드로 파싱하여 실행
    $array_code = '$cHhVk = array(' . $matches[1] . ');';
    eval($array_code);
    echo json_encode($cHhVk, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
} else {
    echo "Not found";
}
