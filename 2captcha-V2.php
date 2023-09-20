<?php

function solve_recaptcha_v2($api_key, $site_key, $page_url, $min_score) {
    $endpoint = 'https://www.2captcha.com/in.php';
    $response_url = 'https://www.2captcha.com/res.php';

    try {
        $ch = curl_init($endpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, [
            'key' => $api_key,
            'method' => 'userrecaptcha',
            'googlekey' => $site_key,
            'pageurl' => $page_url,
            'version' => 'v2',
            'action' => 'verify',
            'min_score' => $min_score
        ]);

        $response = curl_exec($ch);

        if (curl_getinfo($ch, CURLINFO_HTTP_CODE) == 200) {
            if (strpos($response, '|') !== false) {
                $captcha_id = explode('|', $response)[1];

                while (true) {
                    $ch = curl_init($response_url . "?key=$api_key&action=get&id=$captcha_id");
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                    $response = curl_exec($ch);

                    if (curl_getinfo($ch, CURLINFO_HTTP_CODE) == 200) {
                        if (strpos($response, 'OK') === 0) {
                            $response_data = explode('|', substr($response, 3));
                            return $response_data;
                        } elseif (strpos($response, 'CAPCHA_NOT_READY') !== false) {
                            sleep(5);
                        } else {
                            return null;
                        }
                    } else {
                        return null;
                    }
                }
            } else {
                return null;
            }
        } else {
            return null;
        }
    } catch (Exception $e) {
        echo 'Erro na solicitação HTTP: ' . $e->getMessage();
        return null;
    }
}

// Exemplo de uso
$api_key = '00a2a83668057328963310bf8873f55f';
$site_key = '6LcJDCwUAAAAAPZsx3c7deGx7REdi5U3eNERQ_0j';
$page_url = 'https://servicosonline.cpfl.com.br/agencia-webapp';
$min_score = 0.5;

$response_data = solve_recaptcha_v2($api_key, $site_key, $page_url, $min_score);
if ($response_data) {
    // Recaptcha resolvido com sucesso
    echo 'Resultado: ';
    print_r($response_data[0]);

    
} else {
    // Erro ao resolver o recaptcha
    echo 'Erro ao resolver o reCAPTCHA V2';
}


?>