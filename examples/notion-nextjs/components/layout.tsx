import Link from "next/link"

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <ul>
        <Link href="/">Home</Link>
        <br />
        <Link href="/fbbffdea4b544cde91243d79abf9712c">
          fbbffdea4b544cde91243d79abf9712c
        </Link>
        <br />
        <Link href="/afc0a3c837134d11a03a993f0f910304">
          afc0a3c837134d11a03a993f0f910304
        </Link>
      </ul>

      <main>{children}</main>
    </>
  )
}
