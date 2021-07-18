/**
 * 動画のキャプチャを開始する
 */
function start_video_stream() {
    var video = document.getElementById("myVideo"); // 適当にvideoタグのオブジェクトを取得
    // 映像・音声を取得するかの設定
    // 映像はバックカメラ（環境側カメラ）を使用する
    var constrains = { video: { facingMode: "environment" }, audio: false };
    navigator.mediaDevices
        .getUserMedia(constrains)
        .then(function (stream) {
            video.srcObject = stream; // streamはユーザーのカメラとマイクの情報で、これをvideoの入力ソースにする
            video.play();
        })
        .catch(function (err) {
            console.log("An error occured! " + err);
        });
}

// 動画のキャプチャを開始
start_video_stream();
