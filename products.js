/* JK Safety Vision — Shared Product Catalogue
   Product IDs are matched flexibly with homepage product IDs.
*/

window.PRODUCTS = [
  {
    id: "11",
    name: "Hikvision 2MP Dome Camera",
    brand: "Hikvision",
    make: "Hikvision",
    category: "Dome Camera",
    price: 1850,
    old: 2200,
    rating: 4.5,
    photo: "hikvision-2mp-dome",
    image: "hikvision-2mp-dome",
    description: "2MP indoor dome surveillance camera. Confirm exact model and specifications before ordering.",
    specs: {
      Resolution: "2MP",
      Type: "Indoor Dome",
      Brand: "Hikvision"
    }
  },
  {
    id: "cp-plus-2mp-bullet",
    name: "CP PLUS 2MP Bullet Camera",
    brand: "CP PLUS",
    make: "CP PLUS",
    category: "Bullet Camera",
    price: 1650,
    old: 2000,
    rating: 4.4,
    photo: "cp-plus-2mp-bullet",
    image: "cp-plus-2mp-bullet",
    description: "2MP bullet-style surveillance camera. Confirm exact model and specifications before ordering.",
    specs: {
      Resolution: "2MP",
      Type: "Bullet",
      Brand: "CP PLUS"
    }
  },
  {
    id: "hikvision-4ch-dvr",
    name: "Hikvision 4 Channel DVR",
    brand: "Hikvision",
    make: "Hikvision",
    category: "DVR",
    price: 4500,
    old: 5200,
    rating: 4.5,
    photo: "hikvision-4ch-dvr",
    image: "hikvision-4ch-dvr",
    description: "4-channel DVR recorder. Confirm compatibility and exact model before ordering.",
    specs: {
      Channels: "4",
      Type: "DVR Recorder",
      Brand: "Hikvision"
    }
  },
  {
    id: "cp-plus-8ch-dvr",
    name: "CP PLUS 8 Channel DVR",
    brand: "CP PLUS",
    make: "CP PLUS",
    category: "DVR",
    price: 6500,
    old: 7500,
    rating: 4.4,
    photo: "cp-plus-8ch-dvr",
    image: "cp-plus-8ch-dvr",
    description: "8-channel DVR recorder. Confirm compatibility and exact model before ordering.",
    specs: {
      Channels: "8",
      Type: "DVR Recorder",
      Brand: "CP PLUS"
    }
  }
];

/* Flexible product lookup for product.html */
window.getJKSVProductById = function (requestedId) {
  const products = Array.isArray(window.PRODUCTS) ? window.PRODUCTS : [];

  const normalize = function (value) {
    return String(value ?? "")
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]/g, "");
  };

  const wanted = normalize(requestedId);

  if (!wanted) return null;

  // First: exact ID match
  let product = products.find(function (item) {
    return normalize(item.id) === wanted;
  });

  if (product) return product;

  // Next: match by product name, photo, or image identifier
  product = products.find(function (item) {
    return [
      item.name,
      item.photo,
      item.image
    ].some(function (value) {
      return normalize(value) === wanted;
    });
  });

  if (product) return product;

  // Last: support numeric homepage IDs matching the catalogue order
  if (/^\d+$/.test(String(requestedId).trim())) {
    const numericId = Number(requestedId);

    product = products.find(function (item, index) {
      return Number(item.id) === numericId || index + 1 === numericId;
    });
  }

  return product || null;
};