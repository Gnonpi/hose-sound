const { Client } = require('pg')
require('dotenv').config({
  path: '../.env'
})

const pg_config = {
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
}

const testUsers = {
    canLogin: {
      username: 'denis',
      password: 'caca'
    },
    canRegister: {
      username: 'test-register-user',
      email: 'test-register-email',
      password: 'test-register-password'
    }
}

module.exports = {
  pythonCleanDb: async function () {
    const client = new Client(pg_config)
    await client.connect()
    // todo: sql injection with this library?
    const res = await client.query(`
      DELETE 
      FROM hose_usage_hoseuser 
      WHERE username=$1::text;
    `,
      [testUsers.canRegister.username],
      (err, res) => {
        if (err) {
          throw err
        }
        console.log(res)
        client.end()
      }
    )
  },
  loginUser: async function (browser) {
    // todo: browser.globals.devServer of course not available
    const devServer = 'http://localhost:8080/'
    const testUsername = testUsers.canLogin.username
    const testPassword = testUsers.canLogin.password
    browser
      .url(devServer)
browser.getLog('browser', function(logEntriesArray) {
  if (logEntriesArray.length) {
    console.log('Log length: ' + logEntriesArray.length);
    logEntriesArray.forEach(function(log) {
      console.log(
        '[' + log.level + '] ' + log.timestamp + ' : ' + log.message
      );
    });
  }
})
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=l-in-username]', testUsername)
      .setValue('#login-form input[id=l-in-pswd]', testPassword)
      .click('#login-form button[id=b-login]')
      .click('#login-form button[id=b-login]')
      .waitForElementVisible('#displayed-hoses', 2500)
      .assert.urlContains('/u/' + testUsername)
      .assert.elementPresent('main')
  },
  testUsers
}
