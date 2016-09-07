var express = require('express');
var app = express();

app.get('/', function (req, res){
	res.send("Hello World!");
});

app.use('/webapp', express.static('webapp'));

app.listen(3000, function(){
	console.log('Server started on port 3000');
});