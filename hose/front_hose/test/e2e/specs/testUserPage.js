module.exports = {
  beforeEach: function (browser) {
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=in-username]', testUsername)
      .setValue('#login-form input[id=in-pwsd]', testPassword)
      .click('#login-form button[id=b-login]')
      .click('#login-form button[id=b-login]')
      .waitForElementVisible('#displayed-hoses', 2500)
  },
  'user see list': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .assert.elementPresent('#displayed-hoses')
    for (const x of Array(5).keys()) {
      browser
        .assert.elementPresent('#hose-card' + x.toString())
        .assert.elementPresent('.card-body')
    }
    browser
      .end()
  },
  'user go see hose and hit previous page': function (browser) {
    browser
      .end()
  },
  'user try get unowned hose': function (browser) {
    browser
      .end()
  }
}
