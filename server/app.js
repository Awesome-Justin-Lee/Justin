const express = require('express');
const path = require('path');
const cors = require('cors');

const apiRouter =require('./routers/api');

const app = express();

app.use(cors());

app.use(
    express.static(
        path.join(__dirname,'../build')
    )
);

app.use('/api', apiRouter);

app.listen(8000, () => console.log('서버 시작'));