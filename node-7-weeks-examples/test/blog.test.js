var should = require('should');
var mongoskin = require('mongoskin');

describe('BlogModel', function(){

    var db = mongoskin.db('localhost/test');
    var Blog = require('../models/blog')(db);

    describe('#save', function(){
        it('should save without error', function(done) {
            var blog = {title: 'hello world', content:'the content'}
            Blog.save(blog, done);
        });
    })

    describe('#get', function() {
        it('should get without error', function(done) {
            var blog = {title: 'hello world', content: 'the content'};
            Blog.save(blog, function(err, results) {
                if(err) return done(err);
                should.exists(results._id);
                Blog.get(results._id, done);
            })
        })
    })

    describe('#findByTag', function() {
        it('should find by tag without error', function(done) {
            var blog = {title: 'hello tag', content: 'has tags', tags: ['nodejs', 'programming']};
            Blog.save(blog, function(err, data) {
                if(err) {return done(err);}
                Blog.findByTag('nodejs', function(err, results) {
                    if(err) return done(err);
                    should.exists(results);
                    results[0].title.should.equal('hello tag');
                    done();
                })
            })
        });
    })
});
