import axios from 'axios'
import { load } from 'cheerio'
import fs from 'fs'

const baseUrl = 'https://www.reed.co.uk'
const path = '/jobs/developer-jobs-in-london'
const pages = 10

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const getHtml = async (url) => {
  const result = await axios.get(url)
  return load(result.data)
}

const getDetails = async (url) => {
  const $ = await getHtml(url)

  const description = $('.description').text()

  const skills = $('.skills-list')
    .text()
    .trim()
    .replace(/ /g, '')
    .split('\n')
    .join(',')

  return {
    description,
    skills,
  }
}

const getSearchPage = async (url) => {
  console.log('start', url)
  const $ = await getHtml(url)

  const data = []
  const items = $('.job-result-card').toArray()
  for (const item of items) {
    const id = `#${item.attribs.id}`

    const title = $(id + ' .job-result-heading__title')
      .text()
      .trim()
      .replace(/\n/g, '')
    const salary = $(id + ' .job-metadata__item--salary')
      .text()
      .trim()
    const location = $(id + ' .job-metadata__item--location')
      .text()
      .trim()
    const remote = $(id + ' .job-metadata__item--remote')
      .text()
      .trim()
    const type = $(id + ' .job-metadata__item--type')
      .text()
      .trim()

    const link = $(id + ' a.job-result-card__block-link')[0].attribs.href
    const { description, skills } = await getDetails(`${baseUrl}${link}`)
    await wait(500)
    console.log('done', items.indexOf(item))

    data.push({
      title,
      salary,
      location,
      remote,
      type,
      description,
      skills,
    })
  }

  return data
}

const run = async () => {
  let data = []

  for (let i = 1; i <= pages; i++) {
    const url = `${baseUrl}${path}?pageno=${i}`
    const pageData = await getSearchPage(url)
    data = data.concat(pageData)
    await wait(500)
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2))
  }
}

run()
