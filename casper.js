/**
 * Created by zhurui on 15-12-2.
 */
var casper = require('casper').create();

casper.start('http://casperjs.org/', function () {
    this.echo(this.getTitle());
});

casper.thenOpen('http://phantomjs.org', function () {
    this.echo(this.getTitle());
});

casper.run();
