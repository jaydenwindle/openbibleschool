import React, { Component } from "react";

import { Query } from "react-apollo";
import "./App.css";
import gql from "graphql-tag";

const COURSES_QUERY = gql`
  query {
    courses {
      id
      name
      authors {
        id
        name
      }
    }
  }
`;

class App extends Component {
  render() {
    return (
      <div className="App">
        <Query query={COURSES_QUERY}>
          {({ loading, error, data }) => {
            if (loading) return <div>Fetching</div>;
            if (error) return <div>Error</div>;

            const coursesToRender = data.courses;

            return (
              <div>
                <h1
                  style={{
                    fontFamily: "Quicksand, sans-serif",
                    fontWeight: "bold"
                  }}
                >
                  A List of {data.courses.length} Free Online Bible Courses
                </h1>
                {coursesToRender.map(course => (
                  <p
                    key={course.id}
                    style={{
                      fontFamily: "Quicksand, sans-serif",
                      fontSize: 20
                    }}
                  >
                    {course.name} - {course.authors[0].name}
                  </p>
                ))}
              </div>
            );
          }}
        </Query>
      </div>
    );
  }
}

export default App;
