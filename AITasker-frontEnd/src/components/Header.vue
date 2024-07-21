<template>
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
  <header class="header js-header">
    <div class="header__inner">
      <a href="index.html">
        <img src="../assets/龍年賀卡.png" alt="headro" class="logo" />
      </a>
      <div class="header__search md-none">
        <div class="search__container">
          <input type="text" placeholder="Search..." class="search__input" />
          <button class="search__button">
            <i class="material-icons">search</i>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.space {
  height: 2000px;
  background: white;
  padding-top: 50px;
}

body {
  background-color: white;
}

h1 {
  color: orange;
  text-align: center;
}

li {
  list-style: none;
}

.button {
  position: relative;
  display: flex;
  border: solid 0.5px orange;
  border-radius: 10px;
  transition: all 0.3s;
  margin-inline: auto;
  width: 100%;
  height: 50px;
  line-height: 50px;
  background-color: white;
}

.button:hover {
  box-shadow: 3px 3px 0 rgba(22, 22, 22, 0.8);
}

.button__link {
  display: block;
  width: inherit;
  height: inherit;
  font-size: 18px;
  font-weight: 400;
  color: orange;
}

@media screen and (max-width: 768px) {
  .button__link {
    font-size: 14px;
  }
}

/* Header */
.header {
  position: fixed;
  width: 100%;
  z-index: 1000;
  background-color: white;
}

.header.change-color {
  background-color: white;
}

.header__inner {
  max-width: 1440px;
  height: 95px;
  padding-inline: 20px;
  margin-inline: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: solid 1px gray;
}

.logo {
  width: auto;
  height: 60px;
}

.nav__items {
  display: flex;
  justify-content: space-between;
}

.nav__item:not(:first-child) {
  margin-left: 36px;
}

.nav__link {
  font-size: 18px;
  font-weight: medium;
  color: orange;
}

.header__search {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

.search__container {
  display: flex;
  align-items: center;
  border: 1px solid gray;
  border-radius: 5px;
  margin: 0 10px; /* 限制距離邊界10px */
}

.search__input {
  padding: 5px;
  border: none;
  width: 200px;
  border-top-left-radius: 5px;
  border-bottom-left-radius: 5px;
}

.search__button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 10px;
  color: orange; /* 將圖示改成橘色 */
}

.header__button .button {
  width: 100%;
  height: 50px;
  line-height: 50px;
  background-color: white;
  color: orange;
}

@media screen and (max-width: 768px) {
  .hamburger {
    position: fixed;
    z-index: 9999;
    top: 30px;
    right: 15px;
    width: 25px;
    height: 16px;
  }

  .hamburger span {
    position: absolute;
    background-color: orange;
    width: 25px;
    height: 2px;
  }

  .hamburger span:first-child {
    top: 0;
  }

  .hamburger span:nth-child(2) {
    top: 8px;
  }

  .hamburger span:nth-child(3) {
    top: 16px;
  }

  .hamburger.is-active span:first-child {
    top: 15px;
    transform: rotate(45deg);
  }

  .hamburger.is-active span:nth-child(2) {
    opacity: 0;
  }

  .hamburger.is-active span:nth-child(3) {
    top: 15px;
    transform: rotate(-45deg);
  }

  .drawer__menu {
    position: absolute;
    z-index: 5000;
    top: 0;
    left: 0;
    display: none;
    width: 100%;
    height: 100vh;
    background-color: rgba(34, 34, 34, 0.9);
  }

  .drawer__menu__inner {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: inherit;
    height: inherit;
  }

  .drawer__menu__items {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .drawer__menu__item {
    display: inline-block;
    text-align: center;
  }

  .drawer__menu__item:not(:first-child) {
    margin-top: 50px;
  }

  .drawer__item__link {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .drawer__menu__icon {
    width: 14px;
    height: 14px;
  }

  .drawer__menu__link {
    margin-left: 10px;
    font-size: 18px;
    font-weight: medium;
    color: orange;
    display: block !important;
  }

  .drawer__menu__button {
    margin-top: 50px;
    width: 100%;
    height: 50px;
    line-height: 50px;
    background-color: white;
    color: orange;
  }

  .drawer__menu__button .button__link {
    width: 100%;
    height: 50px;
    line-height: 50px;
    color: orange;
  }
}

@media screen and (max-width: 200px) {
  .header__nav {
    display: none; /* 小於400px時隱藏nav */
  }
}
</style>

<script></script>
