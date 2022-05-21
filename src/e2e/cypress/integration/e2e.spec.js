describe('ASE tests', () => {
  before(() => {
    cy.visit('/');
  });

  beforeEach(() => {
    cy.intercept(Cypress.env('api_url')).as('api');
  });

  it('loads successfully', () => {
    cy.get('[name="lang"]').should('be.visible');
    cy.get('[name="code"]').should('be.visible');
    cy.get('[name="mode"]').should('be.visible').and('have.length', 2);
    cy.get('.result').should('not.exist');
    cy.get('.error').should('not.exist');
  });

  it('displays error on empty input', () => {
    cy.get('form').submit();

    cy.wait('@api').its('response.statusCode').should('eq', 406);

    cy.get('.result').should('not.exist');
    cy.get('.error').should('be.visible');
  });

  const langs = ['Java', 'Kotlin', 'Python'];

  langs.forEach((lang) => {
    it(`displays ${lang} result in HTML format`, () => {
      cy.get('[name="lang"]').select(lang);
      cy.get('[name="code"]').type('print()');
      cy.get('[name="mode"]').check('html');
      cy.get('form').submit();

      cy.wait('@api').its('response.statusCode').should('eq', 200);

      cy.get('.error').should('not.exist');
      cy.get('.result').children('html').children('style').should('exist');
      cy.get('.result')
        .children('html')
        .children('pre')
        .children('code')
        .eq(0)
        .should('contain', 'print')
        .and('be.visible');
      cy.get('.result')
        .children('html')
        .children('pre')
        .children('code')
        .eq(1)
        .should('contain', '(')
        .and('be.visible');
      cy.get('.result')
        .children('html')
        .children('pre')
        .children('code')
        .eq(2)
        .should('contain', ')')
        .and('be.visible');
    });

    it(`displays ${lang} result in JSON format`, () => {
      cy.get('[name="lang"]').select(lang);
      cy.get('[name="code"]').type('print()');
      cy.get('[name="mode"]').check('json');
      cy.get('.submit').click();

      cy.wait('@api').its('response.statusCode').should('eq', 200);

      cy.get('.error').should('not.exist');
      cy.get('.result')
        .should('be.visible')
        .and('include.text', '"token":"print"')
        .and('include.text', '"token":"("')
        .and('include.text', '"token":")"');
    });
  });
});
