var exports = module.exports = function(db) {

  var Blog = db.collection('blog');

  function save(blog, callback) {
    if(!blog || !blog.title || !blog.content) {
      return callback(new Error('error blog'));
    }
    Blog.save(blog, callback);
  }

  function findByTag(tag, callback) {
    Blog.find({tags: tag}).toArray(callback);
  }

  function get(id, callback) {
    Blog.findOne({_id: id}, callback);
  }

  return {
    get: get,
    save: save,
    findByTag: findByTag
  }

}
