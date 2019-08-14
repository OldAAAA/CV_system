let videoHeight = 480
let videoWidth = 640
let outputCanvas = document.getElementById("outputCanvas");

let cap = null
let faceCascade = null;
let src = null;
let gray = null;

function run() {

    faceCascade = new cv.CascadeClassifier();
    faceCascade.load("face.xml")

    cap = new cv.VideoCapture(video)
    src = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC4);
    gray = new cv.Mat(videoHeight, videoWidth, cv.CV_8UC1);

    startCamera();
    requestAnimationFrame(detectFace)
}

async function startCamera() {
    let video = document.getElementById("video");
    let stream = await navigator.mediaDevices.getUserMedia({
        video: {
            width: {
                exact: videoWidth
            },
            height: {
                exact: videoHeight
            }
        },
        audio: false
    })
    video.srcObject = stream;
    video.play();
}

var count = 0;
var status = 2;
var limittime = 500;
var lasttime = 0;
var photo_number = 0
var action_map = [ '请眨眼','请张嘴','请笑一笑','请抬头','请低头','请看左边','请看右边']

var action=1


function start() {
    status = 1;
}


function detectFace() {
    // Capture a frame
    cap.read(src);

    //截取视频帧


    // Convert to greyscale
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);


    // Downsample
    let downSampled = new cv.Mat();
    cv.pyrDown(gray, downSampled);
    cv.pyrDown(downSampled, downSampled);

    // Detect faces
    let faces = new cv.RectVector();
    faceCascade.detectMultiScale(downSampled, faces)

    // Draw boxes
    let size = downSampled.size();
    let xRatio = videoWidth / size.width;
    let yRatio = videoHeight / size.height;



    for (let i = 0; i < faces.size(); ++i) {
        let face = faces.get(i);
        let point1 = new cv.Point(face.x * xRatio, face.y * yRatio);
        let point2 = new cv.Point((face.x + face.width) * xRatio, (face.y + face.height) * xRatio);
        cv.rectangle(src, point1, point2, [255, 0, 0, 255])
    }

    // if(faces.size() == 0){
    //     var idname = "bgMusic8"
    //     console.log(idname)
    //     var audio = document.getElementById(idname);
    //     audio.currentTime = 0;
    //     audio.play();
    //     // action += 1;
    // }

    // if(faces.size() > 1){
    //     var idname = "bgMusic11"
    //     console.log(idname)
    //     var audio = document.getElementById(idname);
    //     audio.currentTime = 0;
    //     audio.play();
    //     // action += 1;
    // }


    if(action <=8 && action >2){
        document.getElementById("tip").innerHTML=action_map[action - 2]
    }

    if(status == 0  && faces.size() == 1){
        var time = new Date();
        var nowtime = (new Date()).valueOf();
        if(nowtime - lasttime > limittime && action <= 8){
            photo_number += 1;
            // console.log("截取第%d张图片 现在时间：%s 过去时间：%s",photo_number,nowtime,lasttime)
            lasttime = nowtime
            if(photo_number % 5 == 0 && action <=8 ){
                if(action != 8){
                    var idname = "bgMusic" +action
                    console.log(idname)
                    var audio = document.getElementById(idname);
                    audio.currentTime = 0;
                    audio.play();
                }
                action += 1;
            }

            if(action > 8){
                var idname = "bgMusic10"
                console.log(idname)
                var audio = document.getElementById(idname);
                audio.currentTime = 0;
                audio.play();
                document.getElementById("tip").innerHTML="采集完毕"
                var button = document.getElementById("trigger")
                button.innerHTML = "重新采集"
                action += 1;
            }
        }

    }


    if(faces.size() == 1 && status == 1 && count > 10){
        action = 1
        console.log("开始截图了");
        lasttime =  (new Date()).valueOf();
        status = 0;

        // var idname = "bgMusic9"
        // console.log(idname)
        // var audio = document.getElementById(idname);
        // audio.currentTime = 0;
        // audio.play();

        var idname = "bgMusic" +action
        console.log(idname)
        var audio = document.getElementById(idname);
        audio.currentTime = 0;
        audio.play();
        action += 1;
        console.log(action_map[action - 2])
        document.getElementById("tip").innerHTML=action_map[action - 2].toString()
    }

    count += 1;

    // Free memory
    downSampled.delete()
    faces.delete()

    // Show image
    cv.imshow(outputCanvas, src)

    requestAnimationFrame(detectFace)
}

// Config OpenCV
var Module = {
    locateFile: function (name) {
        let files = {
            "opencv_js.wasm": '/static/opencv/opencv_js.wasm'
        };
        return files[name]
    },
    preRun: [() => {
        Module.FS_createPreloadedFile("/", "face.xml", "/static/opencv/face.xml",
            true, false);
    }],
    postRun: [
        run
    ]
};