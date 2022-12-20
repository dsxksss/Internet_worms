const cheerio = require("cheerio");
const axios = require("axios");
const path = require("path");
const fs = require("fs");
let startApp = new Date().getTime();

(async () => {
  var { data } = await axios.get("https://movie.douban.com/top250", {
    Headers: {
      "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36",
    },
  });
  const $ = cheerio.load(data);

  $(".hd").each(function (i, ele) {
    fs.appendFile(
      path.join(__dirname, "urls.txt"),
    (i+1)+`\t`+$(ele).children("a").text().replace(/\s*/g, "") + "\n",
      (err) => {
        if (err) console.log(err);
      },
    );
  });
  
  let endApp = new Date().getTime();
  console.log("程序执行耗时:\033[32m",((endApp - startApp)*0.001).toFixed(3),"\033[0m秒");
})();