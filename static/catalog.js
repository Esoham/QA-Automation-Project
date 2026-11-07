/* Small, deliberately testable storefront: safe DOM APIs instead of untrusted HTML. */
"use strict";

const form = document.getElementById("filter-form");
const searchInput = document.getElementById("search");
const categoryInput = document.getElementById("category");
const list = document.getElementById("product-list");
const resultsStatus = document.getElementById("results-status");
const errorStatus = document.getElementById("error-status");
const cartStatus = document.getElementById("cart-status");
const cartItems = [];
let currentRequest;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = String(text);
  return node;
}

function renderCart() {
  const amountCents = cartItems.reduce((sum, item) => sum + item.priceCents, 0);
  const count = cartItems.length;
  cartStatus.textContent = "Cart: " + count + " " + (count === 1 ? "item" : "items") +
    " — $" + (amountCents / 100).toFixed(2);
}

function createCard(product) {
  const article = el("article", "product-card");
  const title = el("h2", "");
  const link = el("a", "", product.name);
  link.href = "/product/" + encodeURIComponent(product.id);
  title.append(link);
  article.append(
    title,
    el("p", "description", product.description),
    el("p", "metadata", "Origin: " + product.origin),
    el("p", "metadata", "Category: " + product.category),
    el("p", "price", "$" + Number(product.price).toFixed(2))
  );
  const add = el("button", "", "Add to cart");
  add.type = "button";
  add.setAttribute("aria-label", "Add " + product.name + " to cart");
  add.addEventListener("click", () => {
    cartItems.push({ id: product.id, priceCents: Math.round(Number(product.price) * 100) });
    renderCart();
  });
  article.append(add);
  return article;
}

async function loadProducts() {
  if (currentRequest) currentRequest.abort();
  currentRequest = new AbortController();
  const signal = currentRequest.signal;
  const params = new URLSearchParams({
    search: searchInput.value,
    category: categoryInput.value
  });
  resultsStatus.textContent = "Loading products...";
  errorStatus.hidden = true;
  try {
    const response = await fetch("/api/products?" + params, { signal });
    if (!response.ok) throw new Error("Catalog unavailable");
    const products = await response.json();
    if (!Array.isArray(products)) throw new Error("Unexpected catalog response");
    list.replaceChildren(...products.map(createCard));
    resultsStatus.textContent = products.length + " " +
      (products.length === 1 ? "product" : "products") + " found";
    if (!products.length) list.append(el("p", "empty", "No products match your search."));
  } catch (error) {
    if (error.name === "AbortError") return;
    list.replaceChildren();
    resultsStatus.textContent = "Unable to load products";
    errorStatus.textContent = "Could not load products. Please try again.";
    errorStatus.hidden = false;
  }
}

form.addEventListener("submit", event => {
  event.preventDefault();
  loadProducts();
});
searchInput.addEventListener("input", loadProducts);
categoryInput.addEventListener("change", loadProducts);
document.getElementById("clear-cart").addEventListener("click", () => {
  cartItems.length = 0;
  renderCart();
});
renderCart();
loadProducts();
