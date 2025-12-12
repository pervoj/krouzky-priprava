import Products from "./products";

export default function Home() {
  return (
    <div className="max-w-4xl w-full mx-auto px-4 py-6 grid gap-6">
      <h1 className="text-2xl font-bold">Produkty</h1>
      <Products />
    </div>
  );
}
