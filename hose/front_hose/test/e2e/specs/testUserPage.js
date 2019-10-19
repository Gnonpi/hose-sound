module.exports = {
  before: async function (browser) {
    await browser.globals.pythonCleanDb()
  },
  after: async function (browser) {
    await browser.globals.pythonCleanDb()
  },
  beforeEach: async function (browser) {
    await browser.globals.loginUser(browser)
  },
  'user see list': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .assert.elementPresent('#displayed-hoses')
    for (const x of Array(5).keys()) {
      browser
        .assert.elementPresent('#hose-card-' + x.toString())
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
