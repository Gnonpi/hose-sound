/*
Copy the content of web browser console

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
*/

// const Pool = require('pg').Pool
// const pool = new Pool({
//   user: process.env.DB_USER,
//   host: process.env.DB_HOST,
//   database: process.env.DB_NAME,
//   password: process.env.DB_PASSWORD,
//   port: process.env.DB_PORT,
// })

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
  /*
  before: async function (browser) {
    const client = await pool.connect()
    await client.query(`-- DELETE
      FROM hose_usage_hoseuser u
      WHERE u.username='${testUsers.canRegister.username}';`)
  },
  after: async function (browser) {
    const client = await pool.connect()
    await client.query(`-- DELETE
      FROM hose_usage_hoseuser u
      WHERE u.username='${testUsers.canRegister.username}';`)
  },*/
  'has login and register forms': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .assert.elementPresent('input[id=in-username]')
      .assert.elementPresent('input[id=in-pwsd]')
      .assert.elementPresent('button[id=b-login]')
    browser
      .waitForElementVisible('#register-comp', 5000)
      .assert.elementPresent('#register-form')
      .assert.elementPresent('input[id=in-email]')
      .assert.elementPresent('input[id=in-username]')
      .assert.elementPresent('input[id=in-password1]')
      .assert.elementPresent('input[id=in-password2]')
      .end()
  },
  'user can login': function (browser) {
    const devServer = browser.globals.devServerURL
    const testUsername = testUsers.canLogin.username
    const testPassword = testUsers.canLogin.password
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=in-username]', testUsername)
      .setValue('#login-form input[id=in-pwsd]', testPassword)
      .click('#login-form button[id=b-login]')
      .click('#login-form button[id=b-login]')
      .pause(2500)
    browser
      .assert.urlContains('/u/' + testUsername)
      .assert.elementPresent('main')
      .end()
  },
  'wrong login infornation': function (browser) {
    const devServer = browser.globals.devServerURL
    const wrongUsername = testUsers.canLogin.username
    const wrongPassword = testUsers.canLogin.password + '-wrong'
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=in-username]', wrongUsername)
      .setValue('#login-form input[id=in-pwsd]', wrongPassword)
      .click('#login-form button[id=b-login]')
      .click('#login-form button[id=b-login]')
      .pause(2500)
    browser
      .assert.urlEquals(devServer + '/#/')
      .assert.elementPresent('#login-form')
      .end()
  },
  'user can register': function (browser) {
    const devServer = browser.globals.devServerURL
    const testEmail = testUsers.canRegister.email
    const testUsername = testUsers.canRegister.username
    const testPassword = testUsers.canRegister.password
    browser
      .url(devServer)
      .waitForElementVisible('#register-comp', 5000)
      .setValue('input[id=in-email]', testEmail)
      .setValue('input[id=in-username]', testUsername)
      .setValue('input[id=in-password1]', testPassword)
      .setValue('input[id=in-password2]', testPassword)
      .click('button[id=b-register]')
      .pause(1000)
    browser
      .assert.urlContains('/u/' + testUsername)
      .end()
  }
}
