const http = require('http');
const fs = require('fs');

const server = http.createServer(
    (req,res) => {
        fs.readFile(
            __dirname + '../build/index.html',
            function(err,data) {
                if(err) {
                    console.log(err);

                    res.statusCode = 500;
                    res.end();
                    return;

                }
                console.log('data: ',data);
                res.statusCode = 200;
                res.setHeader('Content-Type', 'text/html; charset=utf-8')
                res.end(data, 'utf-8');
            }
        )
    }
)

server.listen(8000)

app.listen(8000,function(){
    console.log('app listening to port 8000');
});