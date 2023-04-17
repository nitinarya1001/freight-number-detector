let { PythonShell } = require("python-shell");

let options = {
    args: ["E2C06892200065022BA534FD_175730990911862951657526165313.jpeg"],
    pythonPath: "e:/Internships/CRIS internship/OCR (project 1)/.venv/Scripts/python.exe"
}

PythonShell.run("ocr_func.py", options, function (err, results) {
    if (err) {
        console.log(err);
    } else {
        console.log(results[0], results[1]);
        console.log("script done!");
    }
});
