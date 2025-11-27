# Plot Of Gold [![Deploy](https://github.com/taahamohsin/plot-of-gold/actions/workflows/deploy.yml/badge.svg)](https://github.com/taahamohsin/plot-of-gold/actions/workflows/deploy.yml)


This is an [Observable Framework](https://observablehq.com/framework/) app. To install the required dependencies, run:

```
yarn install
```

Then, to start the local preview server, run:

```
yarn dev
```

Then visit <http://localhost:3000> to preview the article.

To deploy the article to GitHub Pages, run:

```
yarn deploy:gh
```


## Command reference

| Command           | Description                                              |
| ----------------- | -------------------------------------------------------- |
| `yarn install`            | Install or reinstall dependencies                |
| `yarn dev`        | Start local preview server                               |
| `yarn build`      | Build your static site, generating `./dist`              |
| `yarn clean`      | Clear the local data loader cache                        |
| `yarn observable` | Run commands like `observable help`                      |
| `yarn deploy:gh`  | Deploy your app to GitHub Pages                          |