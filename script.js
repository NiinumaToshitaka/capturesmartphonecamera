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

// 動画のキャプチャを開始
start_video_stream();
// カメラから画像を取得してcanvasを更新する
update_canvas();
