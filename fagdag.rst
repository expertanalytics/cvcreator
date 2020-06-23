Fagdagsprosjekter
=================

Under finner man en rask oversikt over de forskjellige fagdagsprosjektene
i bedriften.

Chaospy -- Python library for doing Uncertainty Qualification
-------------------------------------------------------------

Chaospy is a numerical tool for performing uncertainty quantification using
polynomial chaos expansions and advanced Monte Carlo methods.
It includes lots of probability theory, variance reduction techniques,
approximations, and Gaussian quadrature.

=============  ================================================================
Lead           Jonathan Feinberg
Repository     `<https://github.com/jonathf/chaospy>`_
Tasks          `<https://github.com/jonathf/chaospy/blob/master/tasks.rst>`_
Keywords       Python, Probability theory, Uncertainty Quantification
=============  ================================================================

Numpoly -- Polynomials represented as numpy data types
------------------------------------------------------

Numpoly is a generic library for creating and manipulating polynomial arrays.

``numpoly`` is a subclass of ``numpy.ndarray`` and as such is compatible with
most ``numpy`` functions, where that makes sense.

=============  ================================================================
Lead           Jonathan Feinberg
Repository     `<https://github.com/jonathf/numpoly>`_
Tasks          `<https://github.com/jonathf/numpoly/blob/master/tasks.rst>`_
Keywords       Python, Numpy, Polynomials
=============  ================================================================

Rasputin -- Tool for generating triangle surface meshes from rasters
--------------------------------------------------------------------

Rasputin in a hybrid C++/Python tool to generate TINs from rasters.

=============  ================================================================
Lead           Ola Skavhaug
Repository     `<https://github.com/expertanalytics/rasputin>`_
Tasks          `<https://github.com/expertanalytics/rasputin/wiki>`_
Keywords       Python, C++, Computational Geometry, Hydrology
=============  ================================================================

lv2-plugins -- Realtime audio processing plugins for music production
--------------------------------------------------------------------

The lv2 plugin project is about writing audio processing plugins for music
production. The plugin in type is `lv2` which can be used on `Linux` and `Mac`.
The code is written in C.
So far we have implemented one simple delay alogrithm.
There are many more effect and plugin types one can implement.
Next steps include: equalizing, high and low pass filtering.

An interesting boundary condition is that all algorithms should be realtime
capable.

Some members in the project plan to also build the physical representation of
the implemented plugin into a guitar pedal. So we can compare the digital vs.
analog signal processing world.

=============  ================================================================
Lead           Vinzenz Gregor Eck
Repository     `<https://github.com/expertanalytics/lv2-plugins>`_
Tasks          `<https://github.com/expertanalytics/lv2-plugins/wiki>`_
Slack Channel  #audio-signal-proc
Keywords       C, Turtle, lv2, signal processing, audio, realtime
=============  ================================================================

Zigarillo (aka The Yak Shaving Project™) -- Efficient event scheduling using inefficient methods
------------------------------------------------------------------------------------------------

Scheduling events can be grueling task. We set out with one ambition:
to solve this problem once and for all.
By putting our best minds together we ascertained that it had to be solved using very low level tools
and cutting edge technology.
In comes Zig.
Zig is a programming language that is so cutting edge that the features we need haven't been implemented yet.
We also ruled GitHub too high level and started using *sourcehut*
as our combined git tool/issue tracker/email list/build tool.
Unfortunately this tool was also too cutting edge.
A less ambitious team might have abandoned ship at this point, but that is not us.
We saw opportunity.

============= =================================================================
Lead          Eigil Skjæveland, Alexander Fleischer
Repository    `<https://git.sr.ht/~af/zigarillo>`_
Tasks         `<https://todo.sr.ht/~af/zigarillo>`_
Slack Channel #zigarillo
Keywords      Zig, sourcehut, git, email
============= =================================================================

bot-api -- Slackbot for scheduling fagdag/formiddag events etc.
---------------------------------------------------------------

@c is XAL's trusty slackbot for scheduling and informing about fagdag/formiddag events.
The bot has a FastAPI backend running on a Heroku server.

============= =================================================================
Lead          Alexander Fleischer
Repository    `<https://github.com/expertanalytics/bot-api>`_
Tasks         `<https://github.com/expertanalytics/bot-api/issues>`_
Slack Channel #schedule-bot
Keywords      Python, FastAPI, PostgreSQL, SQLAlchemy, Slack API, Heroku
============= =================================================================

Bonus Calculator -- Better and more transparent overview of our bonuses
-----------------------------------------------------------------------

The formula that is used to calculate bonuses is the foundation for how we do
things in Expert Analytics. Unfortunately because of Norwegian laws, the
calculations has become more convoluted over time. It has to account for both
yearly and quarterly bonuses, payed out over 5 payouts, accounting for vacation
pay and leave along the way. It is therefore important that the code that
generates the bonuses is as transparent as possible.

=============== ===============================================================
Lead            Jonathan Feinberg, Åsmund Ødegård
Repository      `<https://github.com/expertanalytics/bonus>`_
Tasks           `<https://github.com/expertanalytics/bonus/issues>`_
Keywords        Python, XAL bonuses
=============== ===============================================================
