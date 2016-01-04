#!/usr/bin/env python

from __future__ import print_function

import itertools
import multiprocessing
import os
import subprocess
import string
import threading

common_toc_xpath1 = '//*[contains(concat(" ", @class, " "), " response-title ")]/h:span'
common_toc_xpath2 = '//*[contains(concat(" ", @class, " "), " response ")]//*/h:div[@class="field-content"]/h:p[1]'

data = (
    ('1998',
     "What questions are you asking yourself?",
     'http://edge.org/responses/what-questions-are-you-asking-yourself',
     common_toc_xpath1
     ),
    ('1999',
     "What is the most important invention in the past two thousand years?",
     'http://edge.org/responses/what-is-the-most-important-invention-in-the-past-two-thousand-years',
     common_toc_xpath1
     ),
    ('2000',
     "What is today's most important unreported story?",
     'http://edge.org/responses/what-is-todays-most-important-unreported-story',
     common_toc_xpath1
     ),
    ('2001',
     "What now?",
     'http://edge.org/responses/what-now-',
     common_toc_xpath1
     ),
    ('2001b',
     "What questions have disappeared?",
     'http://edge.org/responses/what-questions-have-disappeared',
     common_toc_xpath1
     ),
    ('2002',
     "What is your question? ... Why?",
     'http://edge.org/responses/what-is-your-question-why',
     common_toc_xpath1
     ),
    ('2003',
     "What are the pressing scientific issues for the nation and the world, and what is your advice on how i can begin to deal with them?",
     'http://edge.org/responses/what-are-the-pressing-scientific-issues-for-the-nation-and-the-world-and-what-is-your-advice-on-how',
     common_toc_xpath1
     ),
    ('2004',
     "What's your law?",
     'http://edge.org/responses/whats-your-law',
     common_toc_xpath1
     ),
    ('2005',
     "What do you believe is true even though you cannot prove it?",
     'http://edge.org/responses/what-do-you-believe-is-true-even-though-you-cannot-prove-it',
     common_toc_xpath2
     ),
    ('2006',
     "What is your dangerous idea?",
     'http://edge.org/responses/what-is-your-dangerous-idea',
     common_toc_xpath1
     ),
    ('2007',
     "What are you optimistic about?",
     'http://edge.org/responses/what-are-you-optimistic-about',
     common_toc_xpath2
     ),
    ('2008',
     "What have you changed your mind about? Why?",
     'http://edge.org/responses/what-have-you-changed-your-mind-about-why',
     common_toc_xpath1
     ),
    ('2009',
     "What will change everything?",
     'http://edge.org/responses/what-will-change-everything',
     common_toc_xpath1
     ),
    ('2010',
     "How is the Internet changing the way you think?",
     'http://edge.org/responses/how-is-the-internet-changing-the-way-you-think',
     common_toc_xpath1
     ),
    ('2011',
     "What scientific concept would improve everybody's cognitive toolkit?",
     'http://edge.org/responses/what-scientific-concept-would-improve-everybodys-cognitive-toolkit',
     common_toc_xpath1
     ),
    ('2012',
     'What is your favorite deep, elegant, or beautiful explanation?',
     'http://edge.org/responses/what-is-your-favorite-deep-elegant-or-beautiful-explanation',
     '//*[contains(concat(" ", @class, " "), " response ")]//*/h:p/h:strong[1]'
     ),
    ('2013',
     'What should we be worried about?',
     'http://edge.org/responses/q2013',
     common_toc_xpath1
     ),
    ('2014',
     'What scientific idea is ready for retirement?',
     'http://edge.org/responses/what-scientific-idea-is-ready-for-retirement',
     common_toc_xpath1
     ),
     ('2015',
     'What do you think about machines that think?',
     'http://edge.org/responses/q2015',
     common_toc_xpath1
     ),
     ('2016',
     'What do you consider the most interesting recent [scientific] news? What makes it important?',
     'http://edge.org/responses/what-do-you-consider-the-most-interesting-recent-scientific-news-what-makes-it',
     common_toc_xpath1
     ),
    )

def group_by_n(iterable, n):
    c = itertools.count()
    for k, g in itertools.groupby(iterable, lambda x: c.next() // n):
         yield list(g)

def create_book(year, title, url, toc_xpath):
    print('Creating Edge book for {}'.format(year))

    in_recipe = 'edgeorg-annual-question.recipe.template'
    out_recipe = 'edgeorg-annual-question-{}.recipe'.format(year)

    with open(in_recipe) as template_f:
        template = string.Template(template_f.read())
        transformed_recipe = template.substitute(year=year, title=title, url=url, toc_xpath=toc_xpath)

    with open(out_recipe, 'w') as out_f:
        out_f.write(transformed_recipe)

    subprocess.check_call(['ebook-convert', out_recipe, 'Edge{}.epub'.format(year)])

    os.remove(out_recipe)

if __name__ == '__main__':
    num_parallel_creations = multiprocessing.cpu_count()
    print('Doing creations in groups of {}'.format(num_parallel_creations))

    threads = []
    for year, title, url, toc_xpath in data[::-1]:
        threads.append(threading.Thread(target=create_book, name=year, args=(year, title, url, toc_xpath)))

    for thread_group in group_by_n(threads, num_parallel_creations):
        for t in thread_group:
            t.start()

        for t in thread_group:
            t.join()
