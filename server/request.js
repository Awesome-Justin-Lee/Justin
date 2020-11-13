const request = require('request');

const certKey = 'kwyjhLhydUm6wYKI9ioJVk8NUkj94o9P';
const date = '2020-11-12';

const requestOptions = {
    uri:'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON',
    qs:{
        authkey : certKey,
        searchdate: date,
        data: 'AP01',
    },
};

request(requestOptions, function (error, reponse, body) {
    if (error) {
        console.log('error:', error)
        return;
    }

    console.log('body: ', body);
    console.log('typeof body: ', typeof body);

    const bodyJSON = JSON.parse(body);
    console.log('bodyJSON: ', bodyJSON);
});