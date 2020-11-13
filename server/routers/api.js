// const express = require('express')

// const router = express.Router();

// router.use(function(req, res, next) {
//     res.send('API 라우터');    
// });

// module.exports = router;

const express = require('express');

const router = express.Router();

router.use(function(req,res,next){
    res.send('API 라우터');
});

router.get('/currency_list/:date', function(req, res, next) {
    
});

module.exports = router;