# ========================================================================
# $File: main.py $
# $Date: 2020-01-17 16:04:44 $
# $Revision: $
# $Creator: Jen-Chieh Shen $
# $Notice: See LICENSE.txt for modification and distribution information
#                   Copyright © 2020 by Shen, Jen-Chieh $
# ========================================================================

from guesslang import Guess

def main():
    """Program Entry point.
    """

    name = Guess().language_name("""
    % Quick sort

      -module (recursion).
      -export ([qsort/1]).

      qsort([]) -> [];
      qsort([Pivot|T]) ->
             qsort([X || X <- T, X < Pivot])
             ++ [Pivot] ++
             qsort([X || X <- T, X >= Pivot]).
    """)


    print(name)  # >>> Erlang

if __name__ == "__main__":
    main()
