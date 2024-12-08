<template>
    <div class="tag">
        <slot>🏷️</slot>
    </div>
</template>

<style>
.tag {
  display: flex;
  flex-flow: row nowrap;
  justify-content: center;
  align-items: center;
  height: fit-content;
  width: fit-content;
  font-size: small;
  border-radius: 16px;
  padding-top: 2px;
  padding-right: 8px;
  padding-bottom: 2px;
  padding-left: 8px;
  margin-top: 1px;
  margin-right: 1px;
  margin-bottom: 1px;
  margin-left: 1px;
  transition-duration: 125ms;
  background-color: white;
  color: black;

  * {
    margin: 0;
    padding: 0;
  }

  p {
    color: inherit;
    background-color: inherit;
  }

  &:hover {
    background-color: #b4dd1e;
    scale: calc(1.05);
    transition-duration: inherit;
  }

  *:hover {
    background-color: inherit;
    transition-duration: inherit;
  }

  div:hover, div > *:hover {
    /* prevent divs and div contents from
    scaling on hover; without this they scale
    to 1.05^2 instead of 1.05^1 */
    scale: unset;
  }

  a:hover, a:visited:hover {
    background-color: inherit;
    color: inherit;
  }
}
</style>