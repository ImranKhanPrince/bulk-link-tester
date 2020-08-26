var readline = require('readline');
var fs = require('fs');
var http = require('http');
var https = require('https');
const { RSA_X931_PADDING } = require('constants');
// var Promise = require('promise');

fs.writeFile('ftpserver.html', '', { flag: 'a+' }, err => {
    if (err) {
        console.log(err);
    }
});

function linkRefiner(mixedTextString) {
    const reCombination = /(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?/g;
    return mixedTextString.match(reCombination);
}
function testlink(url) {
    const method = url.split('://')[0];

    return new Promise((resolve, reject) => {
        if (method == 'http') {
            http.get(url, function (res) {
                // console.log(url, res.statusCode);
                resolve(`<a href="${url}">${url} ${res.statusCode}</a> \n`); //true 1 parameter
            }).on('error', function (e) {
                resolve(`${url} ${e} \n`);
            });
        } else if (method == 'https') {
            https
                .get(url, function (res) {
                    // console.log(url, res.statusCode);
                    resolve(`<a href="${url}">${url} ${res.statusCode}</a> \n`);
                })
                .on('error', function (e) {
                    resolve(`${url} ${e}\n`);
                });
        } else {
            console.log('invalid');
        }
    });
}

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

const inputQuestion = `Type the number to choose option: 
1.Input from text file.
2.Input from witing down the text here. \n
Answer:`;

function textFileProcessor(filename) {
    function fileReadingHandler(err, data) {
        const mixedText = data;
        const linkArray = linkRefiner(mixedText);
        // console.log(linkArray);
        linkArray.forEach(link => {
            testlink(link).then(link => {
                fs.writeFile('ftpserver.html', link, { flag: 'a+' }, err => {
                    console.log(err + '2');
                });
            });
        });
    }
    fs.readFile(filename, 'utf8', fileReadingHandler);
}

rl.question('What is the filename?\nAnswer:', ansFilename => {
    textFileProcessor(__dirname + `/${ansFilename}`);
});

/*else if (answer == 2) {
        rl.question('Paste your wanted links below. \n', pastedLinks => {
            let linkArray = linkRefiner(pastedLinks);
            linkArray.forEach(link => {
                testlink(link).then(link => {
                    fs.writeFile(
                        'ftpserver.html',
                        link,
                        { flag: 'a+' },
                        err => {
                            console.log(err + '2');
                        }
                    );
                });
            });
        });
    } */

// rl.close();

// rl.question(inputQuestion, answerHandler);
