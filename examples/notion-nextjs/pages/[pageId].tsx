import axios from "axios"
import Head from "next/head"
import Image from "next/image"
import { Layout } from "../components/layout"

export default function TestNotionPage({ data }: any) {
  console.log("data", data)
  console.log("process.env.production", process.env.production)
  return (
    <>
      <Head>
        <title>Test Notion Page</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        {data.map((item: any, id: any) => (
          <div key={id}>{renderer(item)}</div>
        ))}
      </Layout>
    </>
  )
}

function renderer(item: any) {
  switch (item.type) {
    case "header":
      return <h1>{item.title}</h1>
      break
    case "sub_header":
      return <h2>{item.title}</h2>
      break
    case "text":
      return <p>{item.title}</p>
      break
    case "image":
      return (
        <Image
          src={item.source}
          alt="image"
          width="200px"
          height="200px"
          objectFit="cover"
        />
      )
      break

    default:
      break
  }
}

export async function getServerSideProps(context: any) {
  const origin = context.req.headers.host
  const { pageId } = context.query
  const API_BASE =
    process.env.NODE_ENV === "production" ? origin : "localhost:3000"
  const API_URL = `http://${API_BASE}/api/retrive-notion-blocks?token_v2=7f03ff0043f4f1b5367552a37201efb3e815abf50eb7170db3df48f1ac4a69fc998e42fbdfcb0f57f57c296226f10d51c96f218ad27e1b6067c68fcd191f55bda1dced6b384f159b9184974eb3bb&pageId=${pageId}`

  console.log("API_URL", API_URL)

  try {
    const res = await axios.get(API_URL)
    return { props: { data: res.data } }
  } catch (error) {
    console.log("error", error)
  }
  return { props: { data: [] } }
}
