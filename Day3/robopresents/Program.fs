namespace parenthesis

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let input = Helper.readLines(argv.[0]).First()
        let move (moveCharacter:char) (currentLocation:int * int) =
            match moveCharacter with
                | '^' -> (fst currentLocation, snd currentLocation + 1)
                | 'v' -> (fst currentLocation, snd currentLocation - 1)
                | '>' -> (fst currentLocation + 1, snd currentLocation)
                | '<' -> (fst currentLocation - 1, snd currentLocation)
                | c -> raise (InvalidOperationException("Don't know how to deal with a particular move character."))

        let rec deliver index santaLocation roboLocation (visitedSet : Set<int * int>) =
            let santaChar = input.Chars(index)
            let newSantaLocation = move santaChar santaLocation
            let roboChar = input.Chars(index + 1)
            let newRoboLocation = move roboChar roboLocation
            let mutable newSet = visitedSet.Add(newSantaLocation).Add(newRoboLocation)
            if index + 3 < input.Length then
                deliver (index + 2) newSantaLocation newRoboLocation newSet
            elif index + 2 < input.Length then
                let lastChar = input.Chars(index + 2)
                let lastLocation = move lastChar newSantaLocation
                newSet <- newSet.Add(lastLocation)
                newSet
            else
                newSet

        let locationsVisited = deliver 0 (0, 0) (0, 0) (Set.empty.Add((0, 0)))
            
        printfn "HousesVisited = %d" locationsVisited.Count
        0
