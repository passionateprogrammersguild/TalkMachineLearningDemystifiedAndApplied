

/* global module:false */
module.exports = function(grunt) {
	var port = grunt.option('port') || 8000;
	var base = grunt.option('base') || '.';

	// Project configuration
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		meta: {
			banner:
				'/*!\n' +
				' * reveal.js <%= pkg.version %> (<%= grunt.template.today("yyyy-mm-dd, HH:MM") %>)\n' +
				' * http://lab.hakim.se/reveal-js\n' +
				' * MIT licensed\n' +
				' *\n' +
				' * Copyright (C) 2016 Hakim El Hattab, http://hakim.se\n' +
				' */'
		},
				
		imagemin: {
			dynamic: {
				files:[{
					expand: true,
					cwd: 'img/src',
					src: ['**/*.{png,jpg,gif}'],
					dest: 'img/',
					
				}]
			}
		}
	});

	// Dependencies	
	grunt.loadNpmTasks('grunt-contrib-imagemin');

	// Default task
	grunt.registerTask( 'default', [ 'imagemin'] );	
};