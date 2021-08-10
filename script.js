/**
 * 動画のキャプチャを開始する
 */
function start_video_stream() {
    // 適当にvideoタグのオブジェクトを取得
    var video = document.getElementById("myVideo");
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
            console.log("An error occured! " + err);
        });
}

// 動画のキャプチャを開始
start_video_stream();
