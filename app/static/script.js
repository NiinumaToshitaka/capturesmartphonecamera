//---------------------------------------------
// 定数定義
//---------------------------------------------
// 保存を行うプログラムがあるURL
const SAVE_URL = "https://192.168.10.103:8081/capture_img";

/** 適当にvideoタグのオブジェクトを取得 */
const video = document.getElementById("myVideo");
/** キャンバスオブジェクト */
const canvas = document.getElementById("picture");
/** キャンバスの幅 */
const canvas_width = canvas.width;
/** キャンバスの高さ */
const canvas_height = canvas.height;

/** 動画のキャプチャを開始する */
function start_video_stream() {
    // 映像・音声を取得するかの設定
    const constrains = {
        // 映像はバックカメラ（環境側カメラ）を使用する
        video: {
            facingMode: "environment",
            width: canvas_width,
            height: canvas_height,
        },
        // 音声は不要なので使用しない
        audio: false,
    };
    navigator.mediaDevices
        .getUserMedia(constrains)
        .then(function (stream) {
            // streamはユーザーのカメラとマイクの情報で、これをvideoの入力ソースにする
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err) {
            console.log(err.name + ": " + err.message);
        });
}

/** カメラから画像を取得してcanvasを更新する */
function update_canvas() {
    document.getElementById("shutter").addEventListener("click", () => {
        const ctx = canvas.getContext("2d");
        // canvasに画像を貼り付ける
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    });
}

/** 画像データの送信ステータス文字列をリセットする */
function reset_sending_status() {
    document.getElementById("sendResult").innerText = "";
}

/**
 * 画像データの送信ステータス文字列を更新する
 * @param {string} status 送信ステータス文字列
 */
function update_sending_status(status) {
    // json形式のデータをパース
    const json_data = JSON.parse(status);

    // パースしたjsonデータを文字列に変換して表示
    document.getElementById("responseJson").innerText =
        JSON.stringify(json_data);

    document.getElementById("sendResult").innerText = json_data.request_status
        ? "OK"
        : "NG";
    // 処理に失敗していた場合はここで終了
    if (!json_data.request_status) {
        document.getElementById("detectionStatus").innerText = "";
        document.getElementById("detectionArea").innerText = "";
        return;
    }

    // 動体検知結果
    const detection_status = json_data.detection_result.detection_status;
    // 動体検知位置
    const detected_area = json_data.detection_result.detected_area;
    document.getElementById("detectionStatus").innerText = detection_status
        ? "YES"
        : "NO";
    switch (detection_status) {
        case true:
            const detected_area_string =
                "(x, y, width, height) = (" +
                detected_area[0] +
                ", " +
                detected_area[1] +
                ", " +
                detected_area[2] +
                ", " +
                detected_area[3] +
                ")";
            document.getElementById("detectionArea").innerText =
                detected_area_string;
            break;
        case false:
            document.getElementById("detectionArea").innerText = "";
            break;
    }
}

/**
 * キャプチャ画像データ(base64)をPOST
 * @param {string} img_base64 base64形式にエンコードされた画像データ
 */
function captureImg(img_base64) {
    // 送信ステータス文字列をリセット
    reset_sending_status();
    let xhr = new XMLHttpRequest();
    const body = new FormData();
    body.append("img", img_base64);
    xhr.open("POST", SAVE_URL, true);
    xhr.onload = () => {
        // 送信ステータス文字列を更新
        update_sending_status(xhr.responseText);
    };
    xhr.send(body);
}

/** サーバへ画像を送信する */
function send() {
    document.getElementById("send").addEventListener("click", () => {
        // Canvasのデータを取得
        // DataURI Schemaが返却される
        // replaceで取得したbase64データのヘッドを取り除く
        const img_base64 = canvas.toDataURL("image/jpeg").replace(/^.*,/, "");
        // 送信
        captureImg(img_base64);
    });
}

// 動画のキャプチャを開始
start_video_stream();
// カメラから画像を取得してcanvasを更新する
update_canvas();
// サーバへ画像を送信する
send();
