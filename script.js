//---------------------------------------------
// 定数定義
//---------------------------------------------
// 保存を行うプログラムがあるURL
const SAVE_URL = 'https://192.168.10.103:8081';

/** 適当にvideoタグのオブジェクトを取得 */
const video = document.getElementById("myVideo");
/** キャンバスオブジェクト */
const canvas = document.getElementById("picture");

/**
 * 動画のキャプチャを開始する
 */
function start_video_stream() {
    // 映像・音声を取得するかの設定
    const constrains = {
        // 映像はバックカメラ（環境側カメラ）を使用する
        video: {
            facingMode: "environment"
        },
        // 音声は不要なので使用しない
        audio: false
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
    document.getElementById("shutter")
        .addEventListener("click", () => {
            const ctx = canvas.getContext("2d");
            // canvasに画像を貼り付ける
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        });
}

/** サーバへ画像を送信する */
function send() {
    document.getElementById("send")
        .addEventListener("click", () => {
            // Canvasのデータを取得
            // DataURI Schemaが返却される
            const hoge = canvas.toDataURL("image/png");

            // 送信情報の設定
            const param = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json; charset=utf-8"
                },
                body: JSON.stringify({ data: hoge })
            };

            // json形式の文字列を出力
            document.getElementById("sendingJsonText").innerText = param.body;

            // サーバへ送信
            sendServer(SAVE_URL, param);
        });
}

/**
 * サーバへJSON送信
 *
 * @param url   {string} 送信先URL
 * @param param {object} fetchオプション
 */
function sendServer(url, param) {
    fetch(url, param)
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            if (json.status) {
                alert("送信に『成功』しました");
                // json.resultにはファイル名が入っている
                // setImage(json.result);
            }
            else {
                alert("送信に『失敗』しました");
                console.log(`[error1] ${json.result}`);
            }
        })
        .catch((error) => {
            alert("送信に『失敗』しました");
            console.log(`[error2] ${error}`);
        });
}

// 動画のキャプチャを開始
start_video_stream();
// カメラから画像を取得してcanvasを更新する
update_canvas();
// サーバへ画像を送信する
send();
